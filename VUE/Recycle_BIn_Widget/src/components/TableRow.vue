<template>
  <!-- Current row -->
  <tr
    :class="{
      'selected-row': selectedRows.includes(row.physicalid)
    }"
  >
    <!-- Checkbox -->
    <td class="height">
      <input
        type="checkbox"
        :value="row.physicalid"
        v-model="computedSelectedRows"
        class="custom-checkbox"
      />
    </td>

    <!-- Dynamic columns -->
    <td
      v-for="header in headers"
      :key="header.key"
      class="p-4"
    >
      <!-- Expandable title column -->
      <template
        v-if="
          header.key === 'attribute[PLMEntity.V_Name]'
          || header.label === 'Title'
        "
      >
        <div
          class="tree-cell-wrapper"
          :style="{ paddingLeft: `${depth * 20}px` }"
        >
          <button
            class="toggle-btn"
            @click.stop="toggleExpand(row)"
          >
            {{
              row.loading
                ? '...'
                : row.expanded
                  ? '-'
                  : '+'
            }}
          </button>

            <!-- Product / 3D cube icon -->
            <span class="product-icon" aria-hidden="true">
              <img src="./icon/Product.png" alt="product">
            </span>

            <span class="product-name-text">
              {{ row[header.key] ?? '-' }}
            </span>
        </div>
      </template>

      <!-- Other columns -->
      <template v-else>
        {{ row[header.key] ?? '-' }}
      </template>
    </td>
  </tr>

  <!-- Recursively render children -->
  <template v-if="row.expanded && row.children?.length">
    <TableRow
      v-for="child in row.children"
      :key="child.physicalid"
      :row="child"
      :headers="headers"
      :depth="depth + 1"
      :selected-rows="selectedRows"
      :toggle-expand="toggleExpand"
      @update:selectedRows="$emit('update:selectedRows', $event)"
    />
  </template>
</template>

<script setup>
import { computed } from 'vue'

defineOptions({
  name: 'TableRow'
})

const props = defineProps({
  row: {
    type: Object,
    required: true
  },

  headers: {
    type: Array,
    required: true
  },

  depth: {
    type: Number,
    default: 0
  },

  selectedRows: {
    type: Array,
    default: () => []
  },

  toggleExpand: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['update:selectedRows'])

const computedSelectedRows = computed({
  get() {
    return props.selectedRows
  },

  set(value) {
    emit('update:selectedRows', value)
  }
})
</script>
