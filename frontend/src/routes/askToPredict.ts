import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export function askToPredict(File: File) {
    // do the axios request here, add to it the file
    const formData = new FormData();
    formData.append("image", File);
    axios.post(routePrefix + "/predict", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then((res) => {
        console.log(res);
    }).catch((err) => {
        console.log(err);
    });

}