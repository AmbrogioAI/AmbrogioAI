import axios from "axios"
import { routePrefix } from "../config/systemVariables"

export default async function deleteChosenModel():Promise<boolean>{
    return new Promise((resolve)=>{
        axios.post(routePrefix+"/removeModel").then(res=>{
            if(res.status === 200){
                resolve(true)
            }else{
                resolve(false)
            }
        }).catch(err=>{
            console.log(err)
            resolve(false)
        })
    })
}