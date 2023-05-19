resource "aws_s3_bucket" "terraform_state" {
  
  bucket = "${var.project_name}-${data.aws_region.current.name}-terraform-state"
  tags = {
    Name        = var.project_name
  }
}

resource "aws_s3_bucket" "code" {
  
  bucket = "${var.project_name}-${data.aws_region.current.name}-code"
  tags = {
    Name        = var.project_name
  }
}

resource "aws_s3_bucket" "raw" {
  
  bucket = "${var.project_name}-${data.aws_region.current.name}-raw"
  tags = {
    Name        = var.project_name
  }
}

resource "aws_s3_bucket_public_access_block" "raw" {
  bucket = aws_s3_bucket.raw.id

  block_public_acls   = false
  block_public_policy = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}