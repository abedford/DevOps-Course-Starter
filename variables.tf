variable "prefix" { 
  description = "The prefix used for all resources in this environment" 
} 

variable "oauth_client_secret" { 
  description = "The client secret to use for oauth" 
} 
 
 
variable "secret_key" { 
  description = "The secret key to use for cookies" 
} 

variable "location" { 
  description = "The Azure location where all resources in this deployment should be created" 
  default     = "uksouth" 
}