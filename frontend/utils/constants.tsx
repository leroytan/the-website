export const BASE_URL = (process.env.DEPLOY_TYPE == 'local'
  ? process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL
  : process.env.DEPLOY_TYPE == 'development'
  ? process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT
  : process.env.DEPLOY_TYPE == 'test'
  ? process.env.NEXT_PUBLIC_API_BASE_URL_TEST
  : process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION) ?? "/api"; // Fallback to local if no match