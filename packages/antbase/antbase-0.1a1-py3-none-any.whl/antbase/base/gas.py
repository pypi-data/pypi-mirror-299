from antbase import Auth, Log

class Gas:
    __development_mode = True
    __service  = Auth.get_script_service() 
    __script   = Auth.get_head_deployment_id() if __development_mode else Auth.get_deployment_id()

    @staticmethod
    def run(function_name, *pargs):
        body = {
            "function":   function_name,
            "parameters": [*pargs],
            "devMode":    Gas.__development_mode
            }
        Log.info(body)
        result = Gas.__service.scripts().run(body=body, scriptId=Gas.__script).execute()
        Log.info(result)
        return result