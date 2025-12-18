<template>
	<!-- <header
		class="sticky flex items-center justify-between top-0 z-10 border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<Breadcrumbs :items="[{ label: __('Home'), route: { name: 'Home' } }]" />
	</header> -->
	<div
		class="d-flex align-items-center"
		style="
			background: linear-gradient(90deg, #6a11cb 3.62%, #2575fc 97.87%);
			color: #fff;
			height: 50px;
		"
	>
		<div class="container d-flex align-items-center justify-content-between">
			<ul class="d-flex align-items-center" style="display: none !important">
				<li class="promobar_socials-item">
					<a class="link" href="#" target="_blank" rel="noopener noreferrer">
						<i class="icon-facebook"></i>
					</a>
				</li>
				<li class="promobar_socials-item">
					<a class="link" href="#" target="_blank" rel="noopener noreferrer">
						<i class="icon-twitter"></i>
					</a>
				</li>
				<li class="promobar_socials-item">
					<a class="link" href="#" target="_blank" rel="noopener noreferrer">
						<i class="icon-instagram"></i>
					</a>
				</li>
			</ul>
			<div
				class="d-flex align-items-center"
				style="
					display: flex;
					justify-content: center;
					align-items: center;
					flex-grow: 1;
					gap: 104px;
					padding-top: 7px;
					padding-bottom: 7px;
					text-align: center;
					vertical-align: middle;
					flex-wrap: wrap;
				"
			>
				<p
					style="
						margin-right: 15px;
						line-height: 1;
						padding-left: 22px;
						padding-right: 22px;
					"
				>
					Try for free!
					<span style="display: none">30 day Trial and Free Lectures</span>
				</p>
				<a
					class="btn btn--yellow"
					href="#"
					id="signUpTrigger"
					style="
						width: 109px;
						height: 33px;
						padding: 0 20px;
						line-height: 1;
						margin: 0;
					"
				>
					<span style="position: relative; top: 1px">Sign Up</span>
				</a>
			</div>
		</div>
	</div>

	<div class="w-full px-5 pt-5 pb-10">
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<div class="text-xl font-bold text-ink-gray-9">
					{{ __('Hey') }}, {{ user.data?.full_name }} 👋
				</div>
				<div>
					<TabButtons v-if="isAdmin" v-model="currentTab" :buttons="tabs" />
					<div
						v-else
						@click="showStreakModal = true"
						class="bg-surface-amber-2 px-2 py-1 rounded-md cursor-pointer"
					>
						<span> 🔥 </span>
						<span class="text-ink-gray-9">
							{{ streakInfo.data?.current_streak }}
						</span>
					</div>
				</div>
			</div>

			<div class="text-lg text-ink-gray-6 leading-6">
				{{ subtitle }}
			</div>
		</div>

		<AdminHome
			v-if="isAdmin && currentTab === 'instructor'"
			:liveClasses="adminLiveClasses"
			:evals="adminEvals"
		/>
		<StudentHome v-else :myLiveClasses="myLiveClasses" />
	</div>
	<Streak v-model="showStreakModal" :streakInfo="streakInfo" />
</template>
<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import {
	Breadcrumbs,
	call,
	createResource,
	TabButtons,
	usePageMeta,
} from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import StudentHome from '@/pages/Home/StudentHome.vue'
import AdminHome from '@/pages/Home/AdminHome.vue'
import Streak from '@/pages/Home/Streak.vue'

const user = inject<any>('$user')
const { brand } = sessionStore()
const evalCount = ref(0)
const currentTab = ref<'student' | 'instructor'>('instructor')
const showStreakModal = ref(false)

onMounted(() => {
	call('lms.lms.utils.get_upcoming_evals').then((data: any) => {
		evalCount.value = data.length
	})
})

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

const myLiveClasses = createResource({
	url: 'lms.lms.utils.get_my_live_classes',
	auto: !isAdmin.value ? true : false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.utils.get_admin_live_classes',
	auto: isAdmin.value ? true : false,
})

const adminEvals = createResource({
	url: 'lms.lms.utils.get_admin_evals',
	auto: isAdmin.value ? true : false,
})

const streakInfo = createResource({
	url: 'lms.lms.utils.get_streak_info',
	auto: true,
})

const subtitle = computed(() => {
	if (isAdmin.value) {
		let liveClassSuffix =
			adminLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix =
			adminEvals.data?.length > 1 ? __('evaluations') : __('evaluation')
		if (adminLiveClasses.data?.length > 0 && adminEvals.data?.length > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
				adminEvals.data.length,
				evalSuffix,
			)
		} else if (adminLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
			)
		} else if (adminEvals.data?.length > 0) {
			return __('You have {0} {1} scheduled.').format(
				adminEvals.data.length,
				evalSuffix,
			)
		}
		return __('Manage your courses and batches at a glance')
	} else {
		let liveClassSuffix =
			myLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix = evalCount.value > 1 ? __('evaluations') : __('evaluation')
		if (myLiveClasses.data?.length > 0 && evalCount.value > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
				evalCount.value,
				evalSuffix,
			)
		} else if (myLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
			)
		} else if (evalCount.value > 0) {
			return __('You have {0} {1} scheduled.').format(
				evalCount.value,
				evalSuffix,
			)
		}
		return __('Resume where you left off')
	}
})

const tabs = [
	{ label: __('Student'), value: 'student' },
	{ label: __('Instructor'), value: 'instructor' },
]

usePageMeta(() => {
	return {
		title: __('Home'),
		icon: brand.favicon,
	}
})
</script>
