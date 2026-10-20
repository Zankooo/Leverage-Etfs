const strategyFiles = ['osnoven.csv', 'vzvod-2x.csv', 'vzvod-3x.csv'] as const

export type StrategyFile = typeof strategyFiles[number]

export interface SimulationCandidate {
  file: string
  total: number
}

export interface SimulationRow {
  best: SimulationCandidate
  second: SimulationCandidate
  third: SimulationCandidate
}

export interface StrategyStatistics {
  count: number
  mean: number | null
  median: number | null
  max: number | null
  min: number | null
}

export type SimulationStatistics = Record<StrategyFile, StrategyStatistics>

export function calculateSimulationStatistics(rows: readonly SimulationRow[]): SimulationStatistics {
  return Object.fromEntries(strategyFiles.map(file => {
    // Uvrstitev se med simulacijami spreminja, zato strategijo poiščemo po datoteki.
    const totals = rows.flatMap(row => {
      const candidate = [row.best, row.second, row.third].find(item => item?.file === file)
      return candidate && Number.isFinite(candidate.total) ? [candidate.total] : []
    }).sort((a, b) => a - b)

    const count = totals.length
    if (count === 0) {
      return [file, { count: 0, mean: null, median: null, max: null, min: null }]
    }

    const middle = Math.floor(count / 2)
    const median = count % 2 === 0
      ? (totals[middle - 1] + totals[middle]) / 2
      : totals[middle]

    return [file, {
      count,
      mean: totals.reduce((sum, value) => sum + value, 0) / count,
      median,
      max: totals[count - 1],
      min: totals[0]
    }]
  })) as SimulationStatistics
}
