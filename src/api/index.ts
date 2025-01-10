import type { AutoUnpackMethod } from '@/types'
import http from '@/utils/http'

export const postMoveMouse = async (data?: { x?: number; y?: number }) => {
  await http.post('/move_mouse', data)
}

export const getMousePosition = async () => {
  const data = await http.get('/mouse_position')
  return data.data
}

export const postRun = async (data: AutoUnpackMethod[]) => {
  return await http.post('/run_start', data)
}
