import { BASE_URL } from "@/utils/constants"
import { TuitionListing } from "@/components/types"
import ClientDashboard from "./_components/clientdashboard"
import TutorDashboard from "./_components/tutordashboard"
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { fetchWithTokenCheck } from "@/utils/tokenVersionMismatch"

// Force dynamic to ensure fresh data
export const dynamic = 'force-dynamic'

interface AssignmentResponse {
  tutorAssignments: TuitionListing[]
  clientAssignments: TuitionListing[]
}

async function getAssignments(isTutor: boolean, accessToken: string): Promise<AssignmentResponse> {
  let tutorResponse: Response | null = null
  if (isTutor) {
    tutorResponse = await fetchWithTokenCheck(`${BASE_URL}/me/applied-assignments`, {
      headers: {
        Cookie: accessToken ? `access_token=${accessToken}` : "",
      },
      cache: 'no-store'
    })
    if (!tutorResponse.ok) {
      throw new Error('Failed to fetch tutor assignments')
    }
  }
  const clientResponse = await fetchWithTokenCheck(`${BASE_URL}/me/created-assignments`, {
    headers: {
      Cookie: accessToken ? `access_token=${accessToken}` : "",
    },
    cache: 'no-store'
  })
  if (!clientResponse.ok) {
    throw new Error('Failed to fetch client assignments')
  }
  return {
    tutorAssignments: tutorResponse ? await tutorResponse.json() : [],
    clientAssignments: await clientResponse.json()
  }
}

export default async function DashboardPage() {
  const cookieStore = await cookies()
  const accessToken = cookieStore.get('access_token')?.value

  if (!accessToken) {
    throw new Error('No access token found')
  }

  // Get user and tutor info
  const meResponse = await fetchWithTokenCheck(`${BASE_URL}/me`, {
    headers: {
      Cookie: accessToken ? `access_token=${accessToken}` : "",
    },
    cache: 'no-store'
  })

  if (!meResponse.ok) {
    throw new Error('Failed to fetch user info')
  }

  const { user, tutor } = await meResponse.json()

  // Get assignments based on user role
  const assignments = await getAssignments(!!tutor, accessToken)
  // Render appropriate dashboard based on user role
  if (tutor) {
    return <TutorDashboard assignments={assignments} />
  }

  return <ClientDashboard assignments={assignments} />
}
