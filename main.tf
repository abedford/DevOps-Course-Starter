terraform { 
  required_providers { 
    azurerm = { 
      source = "hashicorp/azurerm" 
      version = ">= 2.49" 
    } 
  } 
} 
 
provider "azurerm" { 
  features {} 
} 
 
data "azurerm_resource_group" "main" { 
  name     = "CreditSuisse2_AnnieBedford_ProjectExercise" 
} 

resource "azurerm_app_service_plan" "main" { 
  name                = "alb-terx-todo-asp" 
  location            = data.azurerm_resource_group.main.location 
  resource_group_name = data.azurerm_resource_group.main.name 
  kind                = "Linux" 
  reserved            = true 
 
  sku { 
    tier = "Basic" 
    size = "B1" 
  } 
} 
 
resource "azurerm_app_service" "main" { 
  name                = "alb-terx-todo-app-service" 
  location            = data.azurerm_resource_group.main.location 
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
	"OAUTH_CLIENT_ID" = "640c2ac9d976df608c2b"
	"OAUTH_CLIENT_SECRET" = "ef7ae083a8df980361f0dbff6ab3baa23f943245"
	"PORT" = "5000"
	"WEBSITE_HTTPLOGGING_RETENTION_DAYS" = "10"
	"WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
	"WEBSITES_PORT" = 5000
	"MONGODB_CONNECTION_STRING" = "mongodb://${azurerm_cosmosdb_account.main.name}:$@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
	} 
} 

resource "azurerm_storage_account" "main" {
  name                     = "albterxstorageacc"
  resource_group_name      = data.azurerm_resource_group.main.name 
  location                 = data.azurerm_resource_group.main.location 
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "alb-terx-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
  location			  = data.azurerm_resource_group.main.location 
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
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "alb-terx-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  lifecycle { prevent_destroy = true }
}