/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.r2.cloudflarestorage.com",
        port: "",
        pathname: "/teach-honour-excel-website-**/profile_photos/**",
      }
    ]
  },
  rewrites: async () => {
    console.log("Rewrites are being set up based on NEXT_PUBLIC_DEPLOY_TYPE. NODE_ENV is ignored in this case.");
    console.log("NEXT_PUBLIC_DEPLOY_TYPE:", process.env.NEXT_PUBLIC_DEPLOY_TYPE);
    return [
      {
        source: "/api/:path*",
        destination: (() => {
          switch (process.env.NEXT_PUBLIC_DEPLOY_TYPE) {
            case 'local':
              return process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL;
            case 'development':
              return process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT;
            case 'test':
              return process.env.NEXT_PUBLIC_API_BASE_URL_TEST;
            case 'production':
              return process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION;
            default:
              return "/api"; // Fallback to local if no match
          }
        })() + "/:path*",
      },
      {
        source: "/docs",
        destination: "/api/py/docs",  // Not used
      },
      {
        source: "/openapi.json",
        destination: "/api/py/openapi.json",  // Not used
      },
    ];
  },
};

module.exports = nextConfig;
