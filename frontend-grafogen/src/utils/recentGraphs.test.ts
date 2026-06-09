import { beforeEach, describe, expect, it } from 'vitest'
import {
  cacheUploadedGexf,
  loadCachedGexf,
  loadRecentGraphs,
  saveRecentGraph,
} from './recentGraphs'

describe('recentGraphs', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('saves and loads recent entries with newest first', () => {
    saveRecentGraph({
      type: 'G1',
      name: 'G1',
      vertexCount: 10,
      edgeCount: 5,
      source: 'api',
    })
    saveRecentGraph({
      type: 'G2',
      name: 'G2',
      vertexCount: 20,
      edgeCount: 8,
      source: 'api',
    })

    const list = loadRecentGraphs()
    expect(list).toHaveLength(2)
    expect(list[0].type).toBe('G2')
    expect(list[1].type).toBe('G1')
  })

  it('replaces duplicate graph type', () => {
    saveRecentGraph({ type: 'G1', name: 'old', vertexCount: 1, edgeCount: 1, source: 'api' })
    saveRecentGraph({ type: 'G1', name: 'new', vertexCount: 2, edgeCount: 2, source: 'upload' })

    const list = loadRecentGraphs()
    expect(list).toHaveLength(1)
    expect(list[0].name).toBe('new')
    expect(list[0].source).toBe('upload')
  })

  it('caches uploaded gexf by type', () => {
    cacheUploadedGexf('G3', '<gexf></gexf>')
    expect(loadCachedGexf('G3')).toBe('<gexf></gexf>')
    expect(loadCachedGexf('G1')).toBeNull()
  })

  it('returns empty list for corrupt storage', () => {
    localStorage.setItem('grafogen-recent-graphs', '{bad json')
    expect(loadRecentGraphs()).toEqual([])
  })

  it('returns empty list when storage is not an array', () => {
    localStorage.setItem('grafogen-recent-graphs', '{"type":"G1"}')
    expect(loadRecentGraphs()).toEqual([])
  })
})
