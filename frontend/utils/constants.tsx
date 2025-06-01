export const BASE_URL =
process.env.NODE_ENV == null ||
process.env.NODE_ENV === "development"
? `${process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT}`
: process.env.NODE_ENV === "production"
? `${process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION}`
: `/api/`