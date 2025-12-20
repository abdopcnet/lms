<template>
	<FrappeUIProvider>
		<Layout class="isolate text-base">
			<router-view />
		</Layout>
		<InstallPrompt v-if="isMobile && !settings.data?.disable_pwa" />
		<Dialogs />
	</FrappeUIProvider>
</template>
<script setup>
import { FrappeUIProvider } from 'frappe-ui'
import { Dialogs } from '@/utils/dialogs'
import { computed, onUnmounted, ref, watch } from 'vue'
import { useScreenSize } from './utils/composables'
import { usersStore } from '@/stores/user'
import { useSettings } from '@/stores/settings'
import { useRouter } from 'vue-router'
import { posthogSettings } from '@/telemetry'
import DesktopLayout from './components/DesktopLayout.vue'
import MobileLayout from './components/MobileLayout.vue'
import NoSidebarLayout from './components/NoSidebarLayout.vue'
import NavbarLayout from './components/NavbarLayout.vue'
import InstallPrompt from './components/InstallPrompt.vue'

const { isMobile } = useScreenSize()
const router = useRouter()
const noSidebar = ref(false)
const { userResource } = usersStore()
const { settings } = useSettings()

router.beforeEach((to, from, next) => {
	if (to.query.fromLesson || to.path === '/persona') {
		noSidebar.value = true
	} else {
		noSidebar.value = false
	}
	next()
})

// Layout selection - uses top navbar layout for all screen sizes
// NoSidebarLayout is used for lesson pages and persona route
const Layout = computed(() => {
	if (noSidebar.value) {
		return NoSidebarLayout
	}
	// Use NavbarLayout for both desktop and mobile - it has responsive design built-in
	return NavbarLayout
})

onUnmounted(() => {
	noSidebar.value = false
})

watch(userResource, () => {
	if (userResource.data) {
		posthogSettings.reload()
	}
})
</script>
