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

variable "sqsQueueName"{
  description = "ARN da fila de notificacao"
  default = "sqs-video-notification"
}