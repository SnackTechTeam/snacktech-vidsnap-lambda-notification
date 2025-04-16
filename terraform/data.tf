# obter dados da queue sqs
data "aws_sqs_queue" "queue_notification" {
  name = var.sqsQueueName
}