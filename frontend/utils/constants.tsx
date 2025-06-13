export const BASE_URL = (() => {
  console.log(`NEXT_PUBLIC_DEPLOY_TYPE: ${process.env.NEXT_PUBLIC_DEPLOY_TYPE}`);
  return process.env.NEXT_PUBLIC_DEPLOY_TYPE == 'local'
    ? process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL
    : process.env.NEXT_PUBLIC_DEPLOY_TYPE == 'development'
    ? process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT
    : process.env.NEXT_PUBLIC_DEPLOY_TYPE == 'test'
    ? process.env.NEXT_PUBLIC_API_BASE_URL_TEST
    : process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION // Fallback to local if no match
})() ?? '/api';