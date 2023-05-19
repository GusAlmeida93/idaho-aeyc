resource "aws_glue_catalog_database" "database" {
  name = var.project_name
}


resource "aws_glue_crawler" "crawler" {
  database_name = aws_glue_catalog_database.database.name
  name          = var.project_name
  role          = aws_iam_role.role.arn

  s3_target {
    path = "${local.target_bucket}area"         
  }
  s3_target {
    path = "${local.target_bucket}current"
  }
  s3_target {
    path = "${local.target_bucket}datatype"
  }
  s3_target {
    path = "${local.target_bucket}footnote"
  }
  s3_target {
    path = "${local.target_bucket}industry"
  }
  s3_target {
    path = "${local.target_bucket}occupation"
  }
  s3_target {
    path = "${local.target_bucket}seasonal"
  }
  s3_target {
    path = "${local.target_bucket}series"
  }
  s3_target {
    path = "${local.target_bucket}sector"
  }
  s3_target {
    path = "${local.target_bucket}series"
  }
  s3_target {
    path = "${local.target_bucket}fact"
  }
}

