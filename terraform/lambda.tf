
resource "aws_lambda_permission" "allow_sqs" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = data.aws_sqs_queue.queue_notification.arn
  depends_on    = [aws_lambda_function.lambda]
}

resource "aws_lambda_event_source_mapping" "sqs_to_lambda" {
  event_source_arn = data.aws_sqs_queue.queue_notification.arn
  function_name     = aws_lambda_function.lambda.arn
  batch_size        = 1
}


resource "aws_lambda_function" "lambda" {
  filename         = "${path.module}/lambda_function.zip"
  function_name    = "vidsnap-notification"
  role             = data.aws_iam_role.labrole.arn
  handler          = "lambda_function.handler"
  runtime          = "python3.10"
  source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")

  environment {
    variables = {
      MAIL_USER = var.mailUser
      MAIL_PASS = var.mailPass
    }
  }
}
