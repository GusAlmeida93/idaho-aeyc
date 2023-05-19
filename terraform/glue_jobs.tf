resource "aws_glue_job" "get_bls_data_jobs" {

  for_each = {
        area = "area",
        current = "current",
        datatype = "datatype",
        footnote = "footnote",
        industry = "industry",
        occupation = "occupation",
        seasonal = "seasonal",
        sector = "sector",
        series = "series",
  }

  name     = "${var.project_name}-get_bls_data_${each.key}"
  role_arn = aws_iam_role.role.arn
  glue_version = "3.0"
  worker_type = "G.1X"
  number_of_workers = 2

  command {
    script_location = local.script_location
  }

  default_arguments = {
    "--job-language" = "spark"
    "--enable-continuous-cloudwatch-log" = true
    "--enable-metrics" = true
    "--continuous-log-logGroup"  = "/aws-glue/jobs/${var.project_name}-get_bls_data_series/${each.key}/"
    "--targetBucket" = "${local.target_bucket}${each.key}"
    "--url" = "${local.url}${each.key}"
  }
}
