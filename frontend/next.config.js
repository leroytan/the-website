/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.r2.cloudflarestorage.com",
        port: "",
        pathname: "/teach-honour-excel-website-dev/profile_photos/**",
      }
    ]
  },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NEXT_PUBLIC_VERCEL_ENV === "local"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL}/:path*`
            : process.env.NODE_ENV === "development"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT}/:path*`
            : process.env.NODE_ENV === "production"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL_PRODUCTION}/:path*`
            : `/api/:path*`,
      },
      {
        source: "/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT}/py/docs`
            : "/api/py/docs",
      },
      {
        source: "/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? `${process.env.NEXT_PUBLIC_API_BASE_URL_DEVELOPMENT}/py/openapi.json`
            : "/api/py/openapi.json",
      },
    ];
  },
};

module.exports = nextConfig;
