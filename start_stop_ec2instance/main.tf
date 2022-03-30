resource "aws_iam_role" "role_creation"{
  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    }
  )
  name = "John_Wick"
}

resource "aws_iam_policy" "policy_creation"{
  name = "random_policy"
  policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"]
          Resource = "*"
        },
        {
          Effect = "Allow"
          Action = ["ec2:DescribeInstances", "ec2:DescribeRegions", "ec2:StartInstances", "ec2:StopInstances"]
          Resource = "*"
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "attaching_policy"{
  policy_arn = aws_iam_policy.policy_creation.arn
  role = aws_iam_role.role_creation.name
}

resource "aws_lambda_function" "lambda_creation"{
  filename = "lambda.zip"
  handler = "lambda.lambda_handler"
  role = aws_iam_role.role_creation.arn
  function_name = "lambda"

  source_code_hash = filebase64sha256("lambda.zip")
  runtime = "python3.9"
  timeout = 63
}

resource "aws_cloudwatch_event_rule" "event_rule_creation"{
  name = "test_cloud_watch_rule"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "event_rule_target"{
  arn = aws_lambda_function.lambda_creation.arn
  rule = aws_cloudwatch_event_rule.event_rule_creation.name
}

resource "aws_lambda_permission" "lambda_permission"{
  action = "lambda:InvokeFunction"
  statement_id = "AllowExecutionFromCloudWatch"
  function_name = aws_lambda_function.lambda_creation.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.event_rule_creation.arn
}