import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../data/datasources/job_polling_ds.dart' show JobStatus;

/// Widget stepper pour afficher la progression du traitement
class ProcessingStepper extends StatelessWidget {
  final JobStatus currentStatus;

  const ProcessingStepper({
    super.key,
    required this.currentStatus,
  });

  @override
  Widget build(BuildContext context) {
    final steps = [
      _StepData(
        title: EcoStrings.stepOcr,
        description: EcoStrings.stepOcrDesc,
        status: _getStepStatus(JobStatus.ocr),
      ),
      _StepData(
        title: EcoStrings.stepNlp,
        description: EcoStrings.stepNlpDesc,
        status: _getStepStatus(JobStatus.nlp),
      ),
      _StepData(
        title: EcoStrings.stepAcv,
        description: EcoStrings.stepAcvDesc,
        status: _getStepStatus(JobStatus.acv),
      ),
      _StepData(
        title: EcoStrings.stepScore,
        description: EcoStrings.stepScoreDesc,
        status: _getStepStatus(JobStatus.score),
      ),
    ];

    return Column(
      children: steps.map((step) => _buildStep(step)).toList(),
    );
  }

  _StepStatus _getStepStatus(JobStatus stepStatus) {
    if (currentStatus == stepStatus) {
      return _StepStatus.inProgress;
    } else if (_isStepCompleted(stepStatus)) {
      return _StepStatus.completed;
    } else {
      return _StepStatus.pending;
    }
  }

  bool _isStepCompleted(JobStatus stepStatus) {
    final order = [
      JobStatus.ocr,
      JobStatus.nlp,
      JobStatus.acv,
      JobStatus.score,
    ];
    final currentIndex = order.indexOf(currentStatus);
    final stepIndex = order.indexOf(stepStatus);
    return currentIndex > stepIndex || currentStatus == JobStatus.done;
  }

  Widget _buildStep(_StepData step) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Row(
        children: [
          _buildStepIcon(step.status),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  step.title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                Text(
                  step.description,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStepIcon(_StepStatus status) {
    switch (status) {
      case _StepStatus.completed:
        return Container(
          width: 32,
          height: 32,
          decoration: const BoxDecoration(
            color: EcoColors.primaryGreen,
            shape: BoxShape.circle,
          ),
          child: const Icon(Icons.check, color: Colors.white, size: 20),
        );
      case _StepStatus.inProgress:
        return const SizedBox(
          width: 32,
          height: 32,
          child: CircularProgressIndicator(strokeWidth: 3),
        );
      case _StepStatus.pending:
        return Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.radio_button_unchecked,
              color: Colors.grey[600], size: 20),
        );
    }
  }
}

enum _StepStatus { pending, inProgress, completed }

class _StepData {
  final String title;
  final String description;
  final _StepStatus status;

  _StepData({
    required this.title,
    required this.description,
    required this.status,
  });
}
