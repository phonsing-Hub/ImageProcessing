import { Outlet } from 'react-router-dom'

export default function Root() {
  return (
    <main className='container mx-auto h-screen'>
    <Outlet/>
    </main>
  )
}

