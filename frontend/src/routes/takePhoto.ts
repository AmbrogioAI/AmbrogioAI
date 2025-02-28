import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export default async function takePhoto(): Promise<string> {
    return new Promise((resolve, reject) => {
        axios.post(routePrefix+"/takePhoto").then((res) => {
            if (res.status == 200) {
                resolve(res.data);
            } else {
                reject("Error while taking photo");
            }
        }).catch((err) => {
            reject(err);
        });
    });
}