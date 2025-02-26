import { routePrefix } from "../config/systemVariables";
import axios from 'axios';

export async function testLatency(): Promise<number> {
    // start timer 
    const start = Date.now();
    return new Promise((resolve, reject) => {
        axios.get(`${routePrefix}/test`)
            .then(() => {
                // end timer
                const end = Date.now();
                resolve(end - start);
            })
            .catch((err) => {
                console.log(err)
                reject(err);
            });
    });
}