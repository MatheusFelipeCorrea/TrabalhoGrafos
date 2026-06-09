import { describe, expect, it } from 'vitest'
import { buildCommunityMap, colorForCommunity } from './communityColors'

describe('colorForCommunity', () => {
  it('returns stable palette colors', () => {
    expect(colorForCommunity(0)).toBe('#3b82f6')
    expect(colorForCommunity(1)).toBe('#10b981')
    expect(colorForCommunity(-1)).toBe(colorForCommunity(1))
  })
})

describe('buildCommunityMap', () => {
  it('filters rows by graph type', () => {
    const map = buildCommunityMap(
      [
        { login: 'alice', community_id: 2, graph: 'G1' },
        { login: 'bob', community_id: 0, graph: 'G2' },
        { login: 'carol', community_id: 1, graph: 'G1' },
      ],
      'G1',
    )
    expect(map).toEqual({ alice: 2, carol: 1 })
  })
})
