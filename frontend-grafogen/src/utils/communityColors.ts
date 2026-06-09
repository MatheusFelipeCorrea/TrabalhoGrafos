const PALETTE = [
  '#3b82f6',
  '#10b981',
  '#f59e0b',
  '#ef4444',
  '#8b5cf6',
  '#ec4899',
  '#14b8a6',
  '#f97316',
  '#6366f1',
  '#84cc16',
  '#06b6d4',
  '#a855f7',
]

export function colorForCommunity(communityId: number): string {
  return PALETTE[Math.abs(communityId) % PALETTE.length]
}

export function buildCommunityMap(
  rows: { login: string; community_id: number; graph: string }[],
  graphType: string,
): Record<string, number> {
  const map: Record<string, number> = {}
  for (const row of rows) {
    if (row.graph === graphType) {
      map[row.login] = row.community_id
    }
  }
  return map
}
