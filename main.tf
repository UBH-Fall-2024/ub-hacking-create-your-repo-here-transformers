provider "aws" {
  profile = "deepa"         
  region = "us-east-2"  # Or any region you want to use      
}


resource "aws_s3_bucket" "test-bucket-trial" {
  bucket = "ubhack-intervieww"

  tags = {
    Name        = "test bucket"
    Environment = "Dev"
  }
}
