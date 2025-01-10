export type AutoUnpackMethod = { type?: string; description?: string } & (
  | (MoveToMethod & { type: 'moveTo' })
  | (DelayMethod & { type: 'delay' })
  | (ClickMethod & { type: 'click' })
)

export interface MoveToMethod {
  x?: number
  y?: number
}

export interface DelayMethod {
  time?: number // ms
}

export interface ClickMethod {
  key?: 'left' | 'right'
}
