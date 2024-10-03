from antbase._.server_logger.log import Log

a= "aaaaaaaaaaaaa"

Log.log("CRITICAL", "Critical Logging from drive file handler")
Log.log("Jast information")
Log.log(f"Jast aaaaaaaaaaa: {a}!!!")

Log.log("ERROR", "Logging from drive file handler")
Log.log("INFO",  "Logging from drive file handler", "user", "test_user", "action", "file_upload", "status", "success")
Log.log("Hello, ants!")

Log.error("Critical error occurred", "Error message", abc="123", xyz="456")
Log.info("Information message","ants info")
Log.warning("Warning message","ants warning")


Log.pc(False, "This is a precondition error")