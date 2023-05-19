terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
   backend "s3" {
    bucket = "idaho-aeyc-us-east-1-terraform-state"
    key    = "terraform"
    region = "us-east-1"
  }

}


# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}