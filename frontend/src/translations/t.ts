import en from "./en.json";
import it from "./it.json";

export enum Language {
    EN = "en",
    IT = "it"
}

const translations: Record<Language, Record<string, string>> = {
    [Language.EN]: en,
    [Language.IT]: it
};

export function t(key: string, lang: Language): string {
    return translations[lang]?.[key] ?? translations[Language.EN]?.[key] ?? key;
}