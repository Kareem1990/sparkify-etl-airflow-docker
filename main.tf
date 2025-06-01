# ✅ Set the AWS region
provider "aws" {
  region = "us-east-1"
}

# ✅ IAM role that allows Redshift Serverless to assume it
resource "aws_iam_role" "redshift_role" {
  name = "redshift_serverless_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = {
        Service = "redshift.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

# ✅ Attach AmazonS3ReadOnlyAccess policy so Redshift can read data from S3
resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.redshift_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# ✅ Attach custom inline policy to allow access to specific S3 bucket
resource "aws_iam_policy" "sparkify_bucket_policy" {
  name        = "sparkify-data-lake-access"
  description = "Custom policy to allow Redshift to access sparkify-data-lake bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket"
        ],
        Resource = "arn:aws:s3:::sparkify-data-lake"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject"
        ],
        Resource = "arn:aws:s3:::sparkify-data-lake/*"
      }
    ]
  })
}

# ✅ Attach the custom policy to the Redshift IAM role
resource "aws_iam_role_policy_attachment" "custom_s3_policy_attachment" {
  role       = aws_iam_role.redshift_role.name
  policy_arn = aws_iam_policy.sparkify_bucket_policy.arn
}

# ✅ Create Redshift Serverless namespace
resource "aws_redshiftserverless_namespace" "sparkify_namespace" {
  namespace_name       = "sparkify-namespace"
  admin_username       = var.redshift_username
  admin_user_password  = var.redshift_password  # ← ده هو اللي بيتسجل في الكونسول
  iam_roles            = [aws_iam_role.redshift_role.arn]
}

# ✅ Create Security Group that allows Redshift access
resource "aws_security_group" "redshift_sg" {
  name        = "redshift-public-sg"
  description = "Allow Redshift access from anywhere"
  vpc_id      = "vpc-036d5fc0405d50ca5" # ← غيّرها لو عندك VPC مختلف

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # ⚠️ للأمان الأفضل استبدلها بـ ["YOUR_IP/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ✅ Create Redshift Serverless workgroup
resource "aws_redshiftserverless_workgroup" "sparkify_workgroup" {
  workgroup_name       = "sparkify-workgroup"
  namespace_name       = aws_redshiftserverless_namespace.sparkify_namespace.namespace_name
  publicly_accessible  = true
  base_capacity        = 32
  security_group_ids   = [aws_security_group.redshift_sg.id]
}

# ✅ Outputs
output "redshift_endpoint" {
  value = aws_redshiftserverless_workgroup.sparkify_workgroup.endpoint
}

output "redshift_database" {
  value = "dev"
}

output "redshift_username" {
  value     = aws_redshiftserverless_namespace.sparkify_namespace.admin_username
  sensitive = true
}

output "redshift_password" {
  value     = aws_redshiftserverless_namespace.sparkify_namespace.admin_user_password
  sensitive = true
}

# Declare required variables
variable "redshift_username" {
  description = "Admin username for Redshift Serverless"
  type        = string
}

variable "redshift_password" {
  description = "Admin password for Redshift Serverless"
  type        = string
  sensitive   = true
}
