export type AutoUnpackMethod = { id?: string; type?: string; description?: string } & (
  | (MoveToMethod & { type: 'moveTo' })
  | (DelayMethod & { type: 'delay' })
  | (ClickMethod & { type: 'click' })
  | (PressMethod & { type: 'keyPress' })
  | (ContinuousMoveClickMethod & { type: 'continuousMoveClick' })
)

export interface AutoUnpackProduction {
  name?: string
  script?: AutoUnpackMethod[]
  loop?: number
}

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

export interface PressMethod {
  key?: string
}

export interface ContinuousMoveClickMethod {
  x?: number
  y?: number
  count?: number
  spacing?: number
}
