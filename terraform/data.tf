# obter dados da queue sqs
data "aws_sqs_queue" "queue_notification" {
  name = var.sqsQueueName
}

data "aws_iam_role" "labrole" {
  name = "LabRole"
}