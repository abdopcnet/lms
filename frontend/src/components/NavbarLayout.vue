<template>
	<!-- Main container with Edison template style -->
	<div class="lms-app-wrapper">
		<!-- Top navigation bar -->
		<Navbar />
		<!-- Main content area -->
		<main class="lms-main-content">
			<slot />
		</main>
	</div>
</template>

<script setup>
import Navbar from '@/components/Navbar/Navbar.vue'
</script>

<style scoped>
.lms-app-wrapper {
	min-height: 100vh;
	display: flex;
	flex-direction: column;
	background: #fff;
}

.lms-main-content {
	flex: 1;
	padding-top: 20px;
}
</style>
