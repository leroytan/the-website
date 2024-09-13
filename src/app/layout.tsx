import './globals.css'
import { Poppins } from 'next/font/google'

const poppins = Poppins({ 
  weight: ['400', '600', '700', '800'],
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: 'My Single Page Website',
  description: 'A simple single-page website with a burger menu',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${poppins.className} text-gray-800`}>{children}</body>
    </html>
  )
}