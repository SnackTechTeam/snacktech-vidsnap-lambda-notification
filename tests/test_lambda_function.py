import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_function import load_template, send_email, handler

def test_load_template_success(tmp_path):
    # Arrange
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "success.html"
    template_file.write_text("Hello, $name!")
    
    with patch("lambda_function.TEMPLATE_DIR", template_dir):
        # Act
        template = load_template("success")
    
    # Assert
    assert template.safe_substitute({"name": "John"}) == "Hello, John!"

def test_load_template_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_template("nonexistent")

@patch("lambda_function.smtplib.SMTP_SSL")
def test_send_email(mock_smtp):
    # Arrange
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    # Act
    send_email("test@example.com", "Test Subject", "<p>Test Body</p>")
    
    # Assert
    mock_smtp_instance.login.assert_called_once()
    mock_smtp_instance.sendmail.assert_called_once_with(
        os.environ['MAIL_USER'], 
        "test@example.com", 
        'Content-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nFrom: VidSnap Application\nTo: test@example.com\nSubject: Test Subject\n\n<p>Test Body</p>'
    )

@patch("lambda_function.load_template")
@patch("lambda_function.send_email")
def test_handler_success(mock_send_email, mock_load_template):
    # Arrange
    mock_load_template.return_value.safe_substitute.return_value = "<p>Processed</p>"
    event = {
        "Records": [
            {
                "body": json.dumps({
                    "Status": "success",
                    "Email": "user@example.com",
                    "name": "John"
                })
            }
        ]
    }
    
    # Act
    response = handler(event, None)
    
    # Assert
    mock_load_template.assert_called_once_with("success")
    mock_send_email.assert_called_once_with("user@example.com", "Seu vídeo foi processado!", "<p>Processed</p>")
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == "Mensagem processada com sucesso!"

@patch("lambda_function.load_template", side_effect=Exception("Template error"))
def test_handler_template_error(mock_load_template):
    # Arrange
    event = {
        "Records": [
            {
                "body": json.dumps({
                    "Status": "error",
                    "Email": "user@example.com"
                })
            }
        ]
    }
    
    # Act
    response = handler(event, None)
    
    # Assert
    assert response["statusCode"] == 500
    assert "Erro durante processamento" in json.loads(response["body"])