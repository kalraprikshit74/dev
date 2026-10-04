<!-- TableRow.vue -->
<template>
  <!-- 1. Render Current Row -->
  <tr :class="{ 'selected-row': selectedRows.includes(row.physicalid) }">
    <td class="height">
      <input 
        type="checkbox" 
        :value="row.physicalid"
        v-model="computedSelectedRows" 
        class="custom-checkbox"
      />
    </td>
    <td v-for="header in headers" :key="header.key" class="p-4">
      <!-- Title / Expandable Column -->
      <template v-if="header.key === 'attribute[PLMEntity.V_Name]' || header.label === 'Title'">
        <div class="tree-cell-wrapper" :style="{ paddingLeft: `${depth * 20}px` }">
          <button 
            v-if="row.hasChildren || row.children?.length" 
            @click.stop="toggleExpand(row)"
            class="toggle-btn"
          >
            {{ row.loading ? '...' : (row.expanded ? '-' : '+') }}
          </button>
          <span>{{ row[header.key] ?? '-' }}</span>
        </div>
      </template>
      
      <!-- Standard Data Columns -->
      <template v-else>
        {{ row[header.key] ?? '-' }}
      </template>
    </td>
  </tr>

  <!-- 2. RECURSION: Render Child Rows when expanded -->
  <template v-if="row.expanded && row.children?.length">
    <TableRow
      v-for="child in row.children"
      :key="child.physicalid"
      :row="child"
      :headers="headers"
      :depth="depth + 1"
      :selected-rows="selectedRows"
      :toggle-expand="toggleExpand"
      @update:selected-rows="$emit('update:selectedRows',$event)"
    />
  </template>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  row: { type: Object, required: true },
  headers: { type: Array, required: true },
  depth: { type: Number, default: 0 },
  selectedRows: { type: Array, default: () => [] },
  toggleExpand: { type: Function, required: true }
})

const emit = defineEmits(['update:selectedRows'])

// Support v-model two-way binding for checkboxes across deep components
const computedSelectedRows = computed({
  get: () => props.selectedRows,
  set: (val) => emit('update:selectedRows', val)
})
</script>