use crate::{
    error::EvaluationFailure,
    ufc::{Allocation, Assignment, Condition, Flag, Rule, Shard, Split, Variation},
    AttributeValue, Configuration,
};

use super::{eval_assignment::AllocationNonMatchReason, eval_bandits::BanditResult};

pub(super) trait EvalBanditVisitor {
    type AssignmentVisitor<'a>: EvalAssignmentVisitor + 'a
    where
        Self: 'a;

    /// Called when (if) evaluation gets configuration.
    fn on_configuration(&mut self, configuration: &Configuration);

    fn visit_assignment<'a>(&'a mut self) -> Self::AssignmentVisitor<'a>;

    /// Called when bandit key is known.
    fn on_bandit_key(&mut self, key: &str);

    /// Called when result of bandit evaluation is known.
    ///
    /// Note that unlike assignment evaluation, bandit evaluation still returns a variation in case
    /// of failure, so failure and result case are not exclusive.
    fn on_result(&mut self, failure: Result<(), EvaluationFailure>, result: &BanditResult);
}

pub(super) trait EvalAssignmentVisitor {
    // Type-foo here basically means that AllocationVisitor may hold references to EvalFlagVisitor
    // but should not outlive it.
    type AllocationVisitor<'a>: EvalAllocationVisitor + 'a
    where
        Self: 'a;

    /// Called when (if) evaluation gets configuration.
    #[allow(unused_variables)]
    #[inline]
    fn on_configuration(&mut self, configuration: &Configuration) {}

    /// Called when evaluation finds the flag configuration.
    #[allow(unused_variables)]
    #[inline]
    fn on_flag_configuration(&mut self, flag: &Flag) {}

    /// Called before evaluation an allocation.
    fn visit_allocation<'a>(&'a mut self, allocation: &Allocation) -> Self::AllocationVisitor<'a>;

    /// Called when variation has been found for the evaluation.
    #[allow(unused_variables)]
    #[inline]
    fn on_variation(&mut self, variation: &Variation) {}

    /// Called with evaluation result.
    #[allow(unused_variables)]
    #[inline]
    fn on_result(&mut self, result: &Result<Assignment, EvaluationFailure>) {}
}

pub(super) trait EvalAllocationVisitor {
    type RuleVisitor<'a>: EvalRuleVisitor + 'a
    where
        Self: 'a;

    type SplitVisitor<'a>: EvalSplitVisitor + 'a
    where
        Self: 'a;

    /// Called before evaluating a rule.
    fn visit_rule<'a>(&'a mut self, rule: &Rule) -> Self::RuleVisitor<'a>;

    /// Called before evaluating a split.
    fn visit_split<'a>(&'a mut self, split: &Split) -> Self::SplitVisitor<'a>;

    /// Called when allocation evaluation result is known. This functions gets passed either the
    /// split matched, or the reason why this allocation was not matched.
    #[allow(unused_variables)]
    #[inline]
    fn on_result(&mut self, result: Result<&Split, AllocationNonMatchReason>) {}
}

pub(super) trait EvalRuleVisitor {
    /// Called when condition is skipped due to being invalid (e.g., regex cannot be compiled or
    /// server response is ill-formatted).
    ///
    /// `condition` is original server response.
    fn on_condition_skip(&mut self, condition: &serde_json::Value);

    fn on_condition_eval(
        &mut self,
        condition: &Condition,
        attribute_value: Option<&AttributeValue>,
        result: bool,
    );

    #[allow(unused_variables)]
    #[inline]
    fn on_result(&mut self, result: bool) {}
}

pub(super) trait EvalSplitVisitor {
    #[allow(unused_variables)]
    #[inline]
    fn on_shard_eval(&mut self, shard: &Shard, shard_value: u64, matches: bool) {}

    #[allow(unused_variables)]
    #[inline]
    fn on_result(&mut self, matches: bool) {}
}

/// Dummy visitor that does nothing.
///
/// It is designed so that all calls to it are optimized away (zero-cost).
pub(super) struct NoopEvalVisitor;

impl EvalBanditVisitor for NoopEvalVisitor {
    type AssignmentVisitor<'a> = NoopEvalVisitor;

    #[inline]
    fn on_configuration(&mut self, _configuration: &Configuration) {}

    #[inline]
    fn on_bandit_key(&mut self, _key: &str) {}

    #[inline]
    fn visit_assignment<'a>(&'a mut self) -> NoopEvalVisitor {
        NoopEvalVisitor
    }

    #[inline]
    fn on_result(&mut self, _failure: Result<(), EvaluationFailure>, _result: &BanditResult) {}
}

impl EvalAssignmentVisitor for NoopEvalVisitor {
    type AllocationVisitor<'a> = NoopEvalVisitor;

    #[inline]
    fn visit_allocation<'a>(&'a mut self, _allocation: &Allocation) -> Self::AllocationVisitor<'a> {
        NoopEvalVisitor
    }
}

impl EvalAllocationVisitor for NoopEvalVisitor {
    type RuleVisitor<'a> = NoopEvalVisitor;

    type SplitVisitor<'a> = NoopEvalVisitor;

    #[inline]
    fn visit_rule<'a>(&'a mut self, _rule: &Rule) -> Self::RuleVisitor<'a> {
        NoopEvalVisitor
    }

    #[inline]
    fn visit_split<'a>(&'a mut self, _split: &Split) -> Self::SplitVisitor<'a> {
        NoopEvalVisitor
    }
}

impl EvalRuleVisitor for NoopEvalVisitor {
    #[inline]
    fn on_condition_skip(&mut self, _condition: &serde_json::Value) {}

    #[inline]
    fn on_condition_eval(
        &mut self,
        _condition: &Condition,
        _attribute_value: Option<&AttributeValue>,
        _result: bool,
    ) {
    }
}

impl EvalSplitVisitor for NoopEvalVisitor {}
