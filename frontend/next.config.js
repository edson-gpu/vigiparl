/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**.assemblee-nationale.fr" },
    ],
  },
};

module.exports = nextConfig;
