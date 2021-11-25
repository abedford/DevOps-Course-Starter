variable "prefix" { 
  description = "The prefix used for all resources in this environment" 
} 

variable "OAUTH_CLIENT_SECRET" { 
  description = "The client secret to use for oauth" 
} 

variable "LOGGLY_TOKEN" {
  description = "The token for loggly"
}
 
variable "SECRET_KEY" { 
  description = "The secret key to use for cookies" 
} 

variable "location" { 
  description = "The Azure location where all resources in this deployment should be created" 
  default     = "uksouth" 
}