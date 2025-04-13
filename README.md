# snacktech-vidsnap-lambda-notification
Lambda que atuará em enviar notificações por e-mail a usuários do VidSnap quando seus vídeos forem processados com sucesso ou não.

## Pré-requisitos

- AWS CLI configurado
- Terraform instalado
- Python 3.10 ou superior

## Arquivos Principais

### lambda_function.py

Possui todo o código em Python para coletar o evento e fazer o disparo de e-mail que deve vir dentro do evento.

### Terraform

- [`lambda.tf`](terraform/lambda.tf): Constrói a Function a configura o trigger a uma fila SQS que já deve existir
- [`permissions.tf`](terraform/permissions.tf): Configura a role de execução da Lambda Function
- [`provider.tf`](terraform/provider.tf): Define o provedor como AWS
- [`variables.tf`](terraform/variables.tf): Variáveis auxiliares na execução do Terraform

## Configuração

### Terraform

Pelo terminal, a partir da raiz do projeto execute os seguintes comandos:

```sh
cd terraform
terraform init
terraform plan
terraform apply
```

no último comando é necessário escrever "yes" para confirmar a execução.

## Uso

A lambda espera uma mensagem chegar em uma fila SQS para ser disparada.

Faça a publicação de uma mensagem, seguindo esse padrão:

```json 
{
	"Email": "<endereço de e-mail válido>",
	"NomeVideo": "<nome completo do vídeo>",
	"Status": "<FinalizadoComSucesso|FinalizadoComErro>"
}
```

Você pode navegar nos logs da lambda para checar se o processo foi executado com sucesso.