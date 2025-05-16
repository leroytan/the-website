export const BASE_URL =
process.env.NEXT_PUBLIC_VERCEL_ENV == null ||
process.env.NEXT_PUBLIC_VERCEL_ENV === "development"
? `${process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT}`
: process.env.NEXT_PUBLIC_VERCEL_ENV === "production"
? `${process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION}`
: `/api/`