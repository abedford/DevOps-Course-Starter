terraform { 
  required_providers { 
    azurerm = { 
      source = "hashicorp/azurerm" 
      version = ">= 2.49" 
    } 
  } 
  backend "azurerm" {
		resource_group_name  = "CreditSuisse2_AnnieBedford_ProjectExercise"
		storage_account_name = "albterxstorageacc"
		container_name       = "terraform"
		key                  = "terraform.tfstate"
	}
	
} 
 
provider "azurerm" { 
  features {} 
} 
 
data "azurerm_resource_group" "main" { 
  name     = "CreditSuisse2_AnnieBedford_ProjectExercise" 
} 

resource "azurerm_app_service_plan" "main" { 
  name                = "${var.prefix}-alb-terx-todo-asp" 
  location            = var.location 
  resource_group_name = data.azurerm_resource_group.main.name 
  kind                = "Linux" 
  reserved            = true 
 
  sku { 
    tier = "Basic" 
    size = "B1" 
  } 
} 
 
resource "azurerm_app_service" "main" { 
  name                = "${var.prefix}-alb-terx-todo-app-service" 
  location            = var.location 
  resource_group_name = data.azurerm_resource_group.main.name 
  app_service_plan_id = azurerm_app_service_plan.main.id 
 
  site_config { 
    app_command_line = "" 
    linux_fx_version = "DOCKER|anniebedford/todo-app-prod:latest" 
  } 
 
  app_settings = { 
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io" 
	"FLASK_APP" = "todo_app/app"
	"FLASK_ENV" = "production"
	"FLASK_SKIP_LOGIN" = "False"
	"MONGO_CONNECTION" = "mongodb"
	"MONGO_PWD" = "${azurerm_cosmosdb_account.main.primary_key}"
	"MONGO_SRV" = "${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255",
	"MONGO_USER" = "${azurerm_cosmosdb_account.main.name}"
	"MONGO_DB"= "todo_db"
	"OAUTH_CLIENT_ID" = "640c2ac9d976df608c2b"
	"OAUTH_CLIENT_SECRET" = var.oauth_client_secret
	"PORT" = "5000"
	"WEBSITE_HTTPLOGGING_RETENTION_DAYS" = "10"
	"WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
	"WEBSITES_PORT" = 5000
	"MONGODB_CONNECTION_STRING" = "mongodb://${azurerm_cosmosdb_account.main.name}:$@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
  "SECRET_KEY" = var.secret_key
  "LOG_LEVEL"="DEBUG"
  "LOGGLY_TOKEN"= var.loggly_token
	} 
} 

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-alb-terx-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
  location			  = var.location 
  offer_type		  = "Standard"
  kind                = "MongoDB"
  capabilities {
    name = "EnableMongo"
  }
  capabilities { name = "EnableServerless" }
  consistency_policy {
    consistency_level       = "Session"
  }
  geo_location {
    location          = var.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-alb-terx-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  
}