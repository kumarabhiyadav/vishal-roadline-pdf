<template>
  <div class="invoice-form">
    <div class="app-header">
      <div class="header-content">
        <h1>Invoice Generator</h1>
        <p class="header-subtitle">Create professional invoices quickly and efficiently</p>
      </div>
    </div>

    <div class="main-container">
      <!-- Left Panel - Invoice Information -->
      <div class="left-panel">
        <div class="panel-card">
          <div class="card-header">
            <h3><span class="icon">📄</span>Invoice Information</h3>
          </div>
          <div class="card-content">
            <div class="form-grid-2col">
              <div class="form-group">
                <label for="companyName">Company Name</label>
               <input 
      id="companyName"
      v-model="metadata.CompanyName" 
      type="text" 
      :list="'companyNames'" 
      placeholder="Enter company name" 
      required 
      class="form-input"
    />
    <datalist id="companyNames">
      <option v-for="company in companyList" :key="company" :value="company" />
    </datalist>
              </div>
              <div class="form-group">
                <label for="billNumber">Bill Number</label>
                <input 
                  id="billNumber"
                  v-model="metadata.BillNumber" 
                  type="text" 
                  placeholder="Enter bill number" 
                  required 
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="source">Source </label>
                <input 
                  id="source"
                  v-model="metadata.Source" 
                  type="text" 
                  placeholder="Source location" 
                  required 
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="destination">Destination</label>
                <input 
                  id="destination"
                  v-model="metadata.Destination" 
                  type="text" 
                  placeholder="Destination location" 
                  required 
                  class="form-input"
                />
              </div>
            </div>
            <div class="form-group">
              <label for="invoiceDate">Invoice Date</label>
              <input 
                id="invoiceDate"
                v-model="metadata.InvoiceDate" 
                type="date" 
                required 
                class="form-input date-input"
              />
            </div>
          </div>
        </div>

        <!-- Summary Card -->
        <div class="panel-card summary-card">
          <div class="card-header">
            <h3><span class="icon">📊</span>Summary</h3>
          </div>
          <div class="card-content">
            <div class="summary-row">
              <span>Total Entries:</span>
              <span class="summary-value">{{ entries.length }}</span>
            </div>
            <div class="summary-row">
              <span>Transport Charges:</span>
              <span class="summary-value">₹{{ totalTransport.toLocaleString() }}</span>
            </div>
            <div class="summary-row">
              <span>Total Detention:</span>
              <span class="summary-value summary-detention">₹{{ totalDetention.toLocaleString() }}</span>
            </div>
            <div class="summary-row total-row">
              <span>Total Amount:</span>
              <span class="summary-value summary-total">₹{{ totalAmount.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel - Entries -->
      <div class="right-panel">
        <div class="panel-card entries-panel">
          <div class="card-header">
            <h3><span class="icon">📋</span>Invoice Entries</h3>
            <button type="button" @click="addEntry" class="add-entry-btn-header">
              <span class="btn-icon">+</span>
              Add Entry
            </button>
          </div>
          
          <div class="entries-container">
            <div
              v-for="(entry, index) in entries"
              :key="index"
              class="entry-card"
            >
              <div class="entry-header">
                <div class="entry-number">Entry {{ index + 1 }}</div>
                <button 
                  v-if="entries.length > 1" 
                  type="button" 
                  @click="removeEntry(index)"
                  class="remove-btn"
                  title="Remove entry"
                >
                  <span>×</span>
                </button>
              </div>

              <div class="entry-form">
                <div class="entry-row">
                  <div class="form-group">
                    <label>Truck Number</label>
                    <input 
                      v-model="entry.TruckNo" 
                      type="text" 
                      placeholder="e.g., MH-12-AB-1234" 
                      required 
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label>LR Number</label>
                    <input 
                      v-model="entry.LRNo" 
                      type="text" 
                      placeholder="LR Number" 
                      required 
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label>Date</label>
                    <input 
                      v-model="entry.Date" 
                      type="date" 
                      required 
                      class="form-input"
                    />
                  </div>
                </div>

                <div class="entry-row">
                  <div class="form-group">
                    <label>Quantity</label>
                    <input 
                      v-model.number="entry.Quantity" 
                      type="number" 
                      min="1"
                      step="1"
                      placeholder="e.g., 1" 
                      required 
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label>Amount (₹)</label>
                    <input 
                      v-model.number="entry.Rate" 
                      type="number" 
                      min="0" 
                      step="0.01"
                      placeholder="0.00" 
                      required 
                      class="form-input amount-input"
                    />
                  </div>
                  <div class="form-group">
                    <label>Detention (₹)</label>
                    <input 
                      v-model.number="entry.Detention" 
                      type="number" 
                      min="0" 
                      step="0.01"
                      placeholder="0.00" 
                      class="form-input"
                    />
                  </div>
                </div>

                <div class="entry-row">
                  <div class="form-group calculated-amount-group">
                    <label>Calculated Amount</label>
                    <div class="calculated-amount-display">
                      ₹{{ calculateEntryAmount(index).toLocaleString() }}
                      <span class="calculation-breakdown" v-if="entry.Quantity > 1">
                        ({{ entry.Quantity }} × ₹{{ entry.Rate.toLocaleString() }} + ₹{{ entry.Detention.toLocaleString() }})
                      </span>
                    </div>
                  </div>
                </div>

                <div class="form-group">
                  <label>Particulars</label>
                  <textarea
                    v-model="entry.Particulars"
                    placeholder="Enter detailed description of goods/services..."
                    rows="2"
                    required
                    class="form-textarea"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Message -->
    <div v-if="message" class="status-message" :class="messageType">
      <div class="message-content">
        <span class="message-icon">{{ messageType === 'success' ? '✓' : '⚠' }}</span>
        <span>{{ message }}</span>
      </div>
    </div>

    <!-- Action Bar -->
    <div class="action-bar">
      <div class="action-content">
        <div class="action-left">
          <span class="entries-count">{{ entries.length }} {{ entries.length === 1 ? 'entry' : 'entries' }}</span>
          <span class="total-amount">Total: ₹{{ totalAmount.toLocaleString() }}</span>
        </div>
        <div class="action-right">
          <button type="button" @click="addEntry" class="secondary-btn">
            <span class="btn-icon">+</span>
            Add Entry
          </button>
          <button @click="handleSubmit" :disabled="loading || !isFormValid" class="primary-btn">
            <span v-if="loading" class="loading-spinner"></span>
            <span class="btn-text">{{ loading ? "Generating..." : "Generate Invoice" }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>

.calculated-amount-group {
  margin-top: 0.5rem;
}

.calculated-amount-display {
  font-weight: 600;
  color: #059669;
  padding: 0.5rem;
  background: #f0fdf4;
  border-radius: 4px;
  border: 1px solid #bbf7d0;
}

.calculation-breakdown {
  font-size: 0.75rem;
  color: #64748b;
  margin-left: 0.5rem;
  font-weight: normal;
}

.summary-row.total-row {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #cbd5e1;
}

.summary-total {
  font-size: 1.1em;
  font-weight: 700;
}
* {
  box-sizing: border-box;
}

.invoice-form {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f8fafc;
  color: #1e293b;
}

.app-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #1e293b;
}

.header-subtitle {
  color: #64748b;
  margin: 0;
  font-size: 0.85rem;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.left-panel {
  background: #f1f5f9;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  order: 2;
}

.right-panel {
  background: white;
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
  order: 1;
}

.panel-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 1rem;
}

.card-header {
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #374151;
}

.icon {
  font-size: 1rem;
}

.card-content {
  padding: 1rem;
}

.form-grid-2col {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.8rem;
}

.form-input,
.form-textarea {
  padding: 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background: white;
  width: 100%;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.date-input {
  max-width: 100%;
}

.amount-input {
  font-weight: 600;
  color: #059669;
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
  min-height: 60px;
}

.summary-card {
  margin-top: auto;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.85rem;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-value {
  font-weight: 600;
  color: #059669;
}

.summary-detention {
  color: #dc2626;
}

.entries-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.add-entry-btn-header {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: background-color 0.2s;
}

.add-entry-btn-header:hover {
  background: #059669;
}

.entries-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entry-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fafbfc;
  overflow: hidden;
}

.entry-header {
  background: #f3f4f6;
  padding: 0.6rem 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.entry-number {
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
}

.remove-btn {
  background: #ef4444;
  color: white;
  border: none;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  transition: background-color 0.2s;
}

.remove-btn:hover {
  background: #dc2626;
}

.entry-form {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.entry-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.8rem;
}

.amount-group .form-input {
  font-weight: 600;
}

.status-message {
  position: fixed;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  z-index: 1000;
  border-radius: 8px;
  padding: 0.8rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideInUp 0.3s ease-out;
  max-width: 400px;
  margin: 0 auto;
}

.status-message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.message-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  font-size: 0.9rem;
}

.message-icon {
  font-weight: bold;
}

.action-bar {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 0.8rem 1rem;
  box-shadow: 0 -1px 3px 0 rgba(0, 0, 0, 0.1);
  position: sticky;
  bottom: 0;
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.action-left {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #64748b;
  font-size: 0.85rem;
}

.entries-count {
  font-weight: 500;
}

.total-amount {
  font-weight: 600;
  color: #059669;
  font-size: 0.9rem;
}

.action-right {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  justify-content: space-between;
}

.secondary-btn {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s;
  font-size: 0.85rem;
  flex: 1;
  justify-content: center;
}

.secondary-btn:hover {
  background: #e2e8f0;
  border-color: #94a3b8;
}

.primary-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: background-color 0.2s;
  font-size: 0.9rem;
  flex: 1;
  justify-content: center;
}

.primary-btn:hover:not(:disabled) {
  background: #2563eb;
}

.primary-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 0.9rem;
  font-weight: bold;
}

.loading-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #ffffff40;
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Medium screens (tablets) */
@media (min-width: 768px) {
  .main-container {
    flex-direction: row;
  }

  .left-panel {
    width: 300px;
    border-right: 1px solid #e2e8f0;
    border-bottom: none;
    order: 1;
  }

  .right-panel {
    flex: 1;
    order: 2;
  }

  .form-grid-2col {
    grid-template-columns: 1fr 1fr;
  }

  .entry-row {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .action-content {
    flex-direction: row;
    justify-content: space-between;
  }

  .action-left {
    gap: 1.5rem;
  }

  .action-right {
    gap: 1rem;
  }

  .secondary-btn,
  .primary-btn {
    flex: 0;
    padding: 0.6rem 1.25rem;
  }

  .status-message {
    bottom: auto;
    top: 1rem;
    right: 1rem;
    left: auto;
    animation: slideInRight 0.3s ease-out;
  }

  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
}

/* Large screens (desktops) */
@media (min-width: 1024px) {
  .app-header {
    padding: 1.5rem 2rem;
  }

  .header-content h1 {
    font-size: 1.875rem;
  }

  .header-subtitle {
    font-size: 0.9rem;
  }

  .left-panel {
    width: 350px;
    padding: 1.5rem;
  }

  .right-panel {
    padding: 1.5rem;
  }

  .card-header {
    padding: 1rem 1.5rem;
  }

  .card-header h3 {
    font-size: 1rem;
  }

  .card-content {
    padding: 1.5rem;
  }

  .form-group label {
    font-size: 0.875rem;
  }

  .form-input,
  .form-textarea {
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .summary-row {
    font-size: 0.9rem;
  }

  .add-entry-btn-header {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .entry-number {
    font-size: 0.9rem;
  }

  .action-bar {
    padding: 1rem 2rem;
  }

  .action-left {
    font-size: 0.9rem;
  }

  .total-amount {
    font-size: 1rem;
  }
}

/* Scrollbar Styling */
.left-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar,
.entries-container::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track,
.right-panel::-webkit-scrollbar-track,
.entries-container::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.left-panel::-webkit-scrollbar-thumb,
.right-panel::-webkit-scrollbar-thumb,
.entries-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb:hover,
.right-panel::-webkit-scrollbar-thumb:hover,
.entries-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
<script>
import { baseURL } from './contants';

export default {
  data() {
    return {
    companyList:[
        
    ],
      metadata: {
        CompanyName: "",
        BillNumber: "",
        Source: "",
        Destination: "",
        InvoiceDate: "",
      },
      entries: [
        {
          TruckNo: "",
          LRNo: "",
          Date: "",
          Quantity: 1,
          Rate: 0,
          Detention: 0,
          Particulars: "",
        },
      ],
      avoidTotalCalculation: false,
      loading: false,
      message: null,
      messageType: 'success',
    };
  },
  computed: {
    totalAmount() {
      return this.entries.reduce((sum, entry) => {
        const quantity = Number(entry.Quantity) || 0;
        const rate = Number(entry.Rate) || 0;
        const detention = Number(entry.Detention) || 0;
        return sum + (quantity * rate) + detention;
      }, 0);
    },
    totalTransport() {
      return this.entries.reduce((sum, entry) => {
        const quantity = Number(entry.Quantity) || 0;
        const rate = Number(entry.Rate) || 0;
        return sum + (quantity * rate);
      }, 0);
    },
    totalDetention() {
      return this.entries.reduce((sum, entry) => sum + (Number(entry.Detention) || 0), 0);
    },
    isFormValid() {
      // Validate metadata
      if (!this.metadata.CompanyName || 
          !this.metadata.BillNumber || 
          !this.metadata.Source || 
          !this.metadata.Destination || 
          !this.metadata.InvoiceDate) {
        return false;
      }
      
      // Validate all entries
      return this.entries.every(entry => {
        return entry.TruckNo && 
               entry.LRNo && 
               entry.Date && 
               entry.Quantity > 0 && 
               entry.Rate >= 0 && 
               entry.Detention >= 0 && 
               entry.Particulars;
      });
    }
  },
  methods: {
    addEntry() {
      this.entries.push({
        TruckNo: "",
        LRNo: "",
        Date: "",
        Quantity: 1,
        Rate: 0,
        Detention: 0,
        Particulars: "",
      });
    },
    removeEntry(index) {
      this.entries.splice(index, 1);
    },
    calculateEntryAmount(index) {
      const entry = this.entries[index];
      const quantity = Number(entry.Quantity) || 0;
      const rate = Number(entry.Rate) || 0;
      const detention = Number(entry.Detention) || 0;
      return (quantity * rate) + detention;
    },
    async handleSubmit() {
  this.loading = true;
  this.message = null;

  try {
    const response = await fetch(`${baseURL}/generate-invoice`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        metadata: this.metadata,
        entries: this.entries.map(entry => ({
          ...entry,
          Amount: this.calculateEntryAmount(this.entries.indexOf(entry))
        })),
        totals: {
          transport: this.totalTransport,
          detention: this.totalDetention,
          grandTotal: this.totalAmount
        }
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to generate invoice: ${errorText}`);
    }
    
    const blob = await response.blob();
    const filename = this.metadata.BillNumber + ".pdf";

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    this.resetForm(); 
    URL.revokeObjectURL(link.href);

    this.message = `Invoice downloaded: ${filename}`;
    this.messageType = "success";
  } catch (error) {
    this.message = `Error: ${error.message}`;
    this.messageType = "error";
  } finally {
    this.loading = false;
  }
  },
  resetForm() {
  this.metadata = {
    CompanyName: "",
    BillNumber: "",
    Source: "",
    Destination: "",
    InvoiceDate: "",
  };
  this.entries = [
    {
      TruckNo: "",
      LRNo: "",
      Date: "",
      Quantity: 1,
      Rate: 0,
      Detention: 0,
      Particulars: "",
    },
  ];
}
  },
   mounted() {
    // this.fetchAutoFills();
  }

  
};
</script>