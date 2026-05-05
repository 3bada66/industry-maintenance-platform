import { describe, it, expect, vi } from 'vitest'
import { useStatus } from '../../src/composables/useStatus'

// Mock di vue-i18n
vi.mock('vue-i18n', () => ({
  useI18n: () => ({
    t: vi.fn((key) => key)
  })
}))

describe('useStatus', () => {
  const { getStatusSeverity, getStatusColor, getStatusLabel, getStatusStyle, getContrastColor } = useStatus()

  describe('getStatusSeverity', () => {
    it('should return success for green colors', () => {
      expect(getStatusSeverity({ color: '#28a745' })).toBe('success')
      expect(getStatusSeverity({ color: '#22c55e' })).toBe('success')
      expect(getStatusSeverity({ color: 'green' })).toBe('success')
    })

    it('should return danger for red colors', () => {
      expect(getStatusSeverity({ color: '#dc3545' })).toBe('danger')
      expect(getStatusSeverity({ color: '#ef4444' })).toBe('danger')
      expect(getStatusSeverity({ color: 'red' })).toBe('danger')
    })

    it('should return warning for orange colors', () => {
      expect(getStatusSeverity({ color: '#fd7e14' })).toBe('warning')
      expect(getStatusSeverity({ color: '#f97316' })).toBe('warning')
      expect(getStatusSeverity({ color: 'orange' })).toBe('warning')
    })

    it('should return secondary for gray colors', () => {
      expect(getStatusSeverity({ color: '#6c757d' })).toBe('secondary')
      expect(getStatusSeverity({ color: '#64748b' })).toBe('secondary')
      expect(getStatusSeverity({ color: 'gray' })).toBe('secondary')
    })

    it('should return info for blue colors', () => {
      expect(getStatusSeverity({ color: '#0d6efd' })).toBe('info')
      expect(getStatusSeverity({ color: '#3b82f6' })).toBe('info')
      expect(getStatusSeverity({ color: 'blue' })).toBe('info')
    })

    it('should fallback to name-based severity when color is not found', () => {
      expect(getStatusSeverity({ name: 'Active' })).toBe('success')
      expect(getStatusSeverity({ name: 'Inactive' })).toBe('secondary')
      expect(getStatusSeverity({ name: 'Maintenance' })).toBe('warning')
      expect(getStatusSeverity({ name: 'Fault' })).toBe('danger')
    })

    it('should return info for unknown status', () => {
      expect(getStatusSeverity({ name: 'Unknown' })).toBe('info')
      expect(getStatusSeverity({})).toBe('info')
      expect(getStatusSeverity(null)).toBe('info')
      expect(getStatusSeverity(undefined)).toBe('info')
    })
  })

  describe('getStatusColor', () => {
    it('should return the status color if available', () => {
      expect(getStatusColor({ color: '#28a745' })).toBe('#28a745')
      expect(getStatusColor({ color: '#dc3545' })).toBe('#dc3545')
    })

    it('should return default color if no color is provided', () => {
      expect(getStatusColor({ name: 'Active' })).toBe('#64748b')
      expect(getStatusColor({})).toBe('#64748b')
      expect(getStatusColor(null)).toBe('#64748b')
    })
  })

  describe('getStatusLabel', () => {
    it('should return the status name if available', () => {
      expect(getStatusLabel({ name: 'Active' })).toBe('Active')
      expect(getStatusLabel({ name: 'Inactive' })).toBe('Inactive')
    })

    it('should return dash for missing status', () => {
      expect(getStatusLabel({})).toBe('-')
      expect(getStatusLabel(null)).toBe('-')
    })
  })

  describe('getStatusStyle', () => {
    it('should return style object with background color', () => {
      const style = getStatusStyle({ color: '#28a745' })
      expect(style).toHaveProperty('background', '#28a745')
      expect(style).toHaveProperty('color')
      expect(style).toHaveProperty('padding', '0.2rem 0.5rem')
      expect(style).toHaveProperty('borderRadius', '4px')
      expect(style).toHaveProperty('fontSize', '0.875rem')
      expect(style).toHaveProperty('fontWeight', '500')
    })

    it('should return empty object for null status', () => {
      expect(getStatusStyle(null)).toEqual({})
    })
  })

  describe('getContrastColor', () => {
    it('should return black for light backgrounds', () => {
      expect(getContrastColor('#ffffff')).toBe('#000000')
      expect(getContrastColor('#f0f0f0')).toBe('#000000')
      expect(getContrastColor('#28a745')).toBe('#ffffff') // verde scuro
    })

    it('should return white for dark backgrounds', () => {
      expect(getContrastColor('#000000')).toBe('#ffffff')
      expect(getContrastColor('#333333')).toBe('#ffffff')
      expect(getContrastColor('#dc3545')).toBe('#ffffff') // rosso scuro
    })

    it('should handle hex colors without #', () => {
      expect(getContrastColor('ffffff')).toBe('#000000')
      expect(getContrastColor('000000')).toBe('#ffffff')
    })
  })
}) 