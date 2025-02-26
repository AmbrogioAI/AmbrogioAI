import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export async function getModel(){
    const res = await axios.get(routePrefix+"/currentModel")
    if(res.status === 200 && res.data["model"] != null){
        return res.data["model"]
    }
    return null
}