import React, { useState } from "react";
import "../styling/Calendar.css";

export default function Calendar({ selectedDate, onDateChange }) {
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [currentDate, setCurrentDate] = useState(selectedDate || new Date());

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const handlePreviousDay = () => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() - 1);
    setCurrentDate(newDate);
    onDateChange?.(newDate);
  };

  const handleNextDay = () => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() + 1);
    setCurrentDate(newDate);
    onDateChange?.(newDate);
  };

  const handleCurrentDateClick = () => {
    setShowDatePicker(true);
  };

  const handleDatePickerChange = (event) => {
    const dateValue = event.target.value;
    const [year, month, day] = dateValue.split('-');
    const newDate = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
    setCurrentDate(newDate);
    onDateChange?.(newDate);
    setShowDatePicker(false);
  };

  const handleDatePickerClose = () => {
    setShowDatePicker(false);
  };

  const formatDateForInput = (date) => {
    return date.toISOString().split('T')[0];
  };

  return (
    <div className="calendar-container">
      <button className="calendar-nav-btn" onClick={handlePreviousDay}>
        ←
      </button>
      
      <button className="calendar-current-btn" onClick={handleCurrentDateClick}>
        {formatDate(currentDate)}
      </button>
      
      <button className="calendar-nav-btn" onClick={handleNextDay}>
        →
      </button>

      {showDatePicker && (
        <div className="date-picker-overlay" onClick={handleDatePickerClose}>
          <div className="date-picker-modal" onClick={(e) => e.stopPropagation()}>
            <input
              type="date"
              value={formatDateForInput(currentDate)}
              onChange={handleDatePickerChange}
              className="date-picker-input"
              autoFocus
            />
            <button className="date-picker-close" onClick={handleDatePickerClose}>
              ×
            </button>
          </div>
        </div>
      )}
    </div>
  );
}