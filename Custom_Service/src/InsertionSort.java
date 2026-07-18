public class InsertionSort {
	// Insertion sort implementation for an array of integers
	public static void insertionSort(int[] arr) {
		int n = arr.length;
		for (int i = 1; i < n; i++) {
			int key = arr[i];
			int j = i - 1;
			// Move elements of arr[0..i-1], that are greater than key, to one position ahead
			while (j >= 0 && arr[j] > key) {
				arr[j + 1] = arr[j];
				j = j - 1;
			}
			arr[j + 1] = key;
		}
	}

	
	public static void printArray(int[] arr) {
		for (int num : arr) {
			System.out.print(num + " ");
		}
		System.out.println();
	}

	public static void main(String[] args) {
		int[] arr = {64, 25, 12, 22, 11};
		System.out.println("Original array:");
		printArray(arr);
		insertionSort(arr);
		System.out.println("Sorted array:");
		printArray(arr);
	}
}
