locals {

    script_location = "s3://${aws_s3_bucket.code.bucket}/idaho-aeyc/jobs/get_bls_data.py"

    target_bucket = "s3://${aws_s3_bucket.raw.bucket}/"

    url = "https://download.bls.gov/pub/time.series/oe/oe."

}