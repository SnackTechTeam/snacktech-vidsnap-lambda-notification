variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "mailUser"{
  description = "E-mail usado como remetente pela Lambda"
  default = ""
}

variable "mailPass"{
  description = "Senha de App configurado para o endereço de e-mail"
  default = ""
}

variable "sqsQueueArn"{
  description = "ARN da fila de notificacao"
  default = "arn:aws:sqs:us-east-1:000000000000:notificacao-email"
}