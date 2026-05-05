/**
 * Unit tests for the useStatus composable.
 * Owner: Praise-God Tobby (QA/Test Engineer, 2309116418)
 *
 * These tests cover the pure logic functions in useStatus:
 * getContrastColor, getStatusSeverity, getStatusColor, getStatusLabel.
 */
import { describe, it, expect } from 'vitest'
import { useStatus } from '../useStatus.js'

const { getContrastColor, getStatusSeverity, getStatusColor, getStatusLabel } = useStatus()

// ---------------------------------------------------------------------------
// getContrastColor
// ---------------------------------------------------------------------------
describe('getContrastColor', () => {
  it('returns white text for a pure black background', () => {
    expect(getContrastColor('#000000')).toBe('#ffffff')
  })

  it('returns black text for a pure white background', () => {
    expect(getContrastColor('#ffffff')).toBe('#000000')
  })

  it('returns white text for a dark red', () => {
    expect(getContrastColor('#dc2626')).toBe('#ffffff')
  })

  it('returns black text for a light yellow', () => {
    expect(getContrastColor('#fef9c3')).toBe('#000000')
  })
})

// ---------------------------------------------------------------------------
// getStatusSeverity — based on color property
// ---------------------------------------------------------------------------
describe('getStatusSeverity — color-based', () => {
  it('returns "info" when status is null', () => {
    expect(getStatusSeverity(null)).toBe('info')
  })

  it('returns "info" when status is undefined', () => {
    expect(getStatusSeverity(undefined)).toBe('info')
  })

  it('maps #28a745 (green) to "success"', () => {
    expect(getStatusSeverity({ color: '#28a745' })).toBe('success')
  })

  it('maps #ef4444 (red) to "danger"', () => {
    expect(getStatusSeverity({ color: '#ef4444' })).toBe('danger')
  })

  it('maps #f97316 (orange) to "warning"', () => {
    expect(getStatusSeverity({ color: '#f97316' })).toBe('warning')
  })

  it('maps #3b82f6 (blue) to "info"', () => {
    expect(getStatusSeverity({ color: '#3b82f6' })).toBe('info')
  })

  it('maps #64748b (gray) to "secondary"', () => {
    expect(getStatusSeverity({ color: '#64748b' })).toBe('secondary')
  })

  it('maps named color "red" to "danger"', () => {
    expect(getStatusSeverity({ color: 'red' })).toBe('danger')
  })

  it('maps named color "green" to "success"', () => {
    expect(getStatusSeverity({ color: 'green' })).toBe('success')
  })
})

// ---------------------------------------------------------------------------
// getStatusSeverity — based on name property (fallback)
// ---------------------------------------------------------------------------
describe('getStatusSeverity — name-based fallback', () => {
  it('maps "active" to "success"', () => {
    expect(getStatusSeverity({ name: 'active' })).toBe('success')
  })

  it('maps "operational" to "success"', () => {
    expect(getStatusSeverity({ name: 'operational' })).toBe('success')
  })

  it('maps "maintenance" to "warning"', () => {
    expect(getStatusSeverity({ name: 'maintenance' })).toBe('warning')
  })

  it('maps "fault" to "danger"', () => {
    expect(getStatusSeverity({ name: 'fault' })).toBe('danger')
  })

  it('maps "error" to "danger"', () => {
    expect(getStatusSeverity({ name: 'error' })).toBe('danger')
  })

  it('maps "inactive" to "secondary"', () => {
    expect(getStatusSeverity({ name: 'inactive' })).toBe('secondary')
  })

  it('maps "stock" to "info"', () => {
    expect(getStatusSeverity({ name: 'stock' })).toBe('info')
  })

  it('maps Italian "guasto" to "danger"', () => {
    expect(getStatusSeverity({ name: 'guasto' })).toBe('danger')
  })

  it('maps Italian "manutenzione" to "warning"', () => {
    expect(getStatusSeverity({ name: 'manutenzione' })).toBe('warning')
  })

  it('returns "info" for an unknown status name', () => {
    expect(getStatusSeverity({ name: 'xyz-unknown' })).toBe('info')
  })
})

// ---------------------------------------------------------------------------
// getStatusColor
// ---------------------------------------------------------------------------
describe('getStatusColor', () => {
  it('returns default gray when status is null', () => {
    expect(getStatusColor(null)).toBe('#64748b')
  })

  it('returns the color property when present', () => {
    expect(getStatusColor({ color: '#ff0000' })).toBe('#ff0000')
  })

  it('returns default gray when status has no color property', () => {
    expect(getStatusColor({ name: 'active' })).toBe('#64748b')
  })
})

// ---------------------------------------------------------------------------
// getStatusLabel
// ---------------------------------------------------------------------------
describe('getStatusLabel', () => {
  it('returns "-" when status is null', () => {
    expect(getStatusLabel(null)).toBe('-')
  })

  it('returns the name property', () => {
    expect(getStatusLabel({ name: 'Active' })).toBe('Active')
  })

  it('returns "-" when name property is missing', () => {
    expect(getStatusLabel({ color: '#ff0000' })).toBe('-')
  })
})
