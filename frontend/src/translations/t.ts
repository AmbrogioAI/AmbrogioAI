import en from "./en.json";
import it from "./it.json";

export enum Language {
    EN = "en",
    IT = "it"
}

export function t(key: string,lang:Language): string {
    let translation = "";
    switch(lang){
        case Language.EN:
            translation = en[key];
            break;
        case Language.IT:
            translation = it[key];
            break;
    }
    return translation;
}