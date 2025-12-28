import 'package:flutter/material.dart';
import '../../../../core/constants/typography.dart';

/// Barre de recherche moderne avec debounce
class SearchBarWidget extends StatefulWidget {
  final ValueChanged<String> onSearchChanged;
  final String? hintText;

  const SearchBarWidget({
    super.key,
    required this.onSearchChanged,
    this.hintText,
  });

  @override
  State<SearchBarWidget> createState() => _SearchBarWidgetState();
}

class _SearchBarWidgetState extends State<SearchBarWidget> {
  final TextEditingController _controller = TextEditingController();
  final FocusNode _focusNode = FocusNode();
  bool _hasText = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _onTextChanged() {
    setState(() {
      _hasText = _controller.text.isNotEmpty;
    });
    widget.onSearchChanged(_controller.text);
  }

  void _clearText() {
    _controller.clear();
    _focusNode.unfocus();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 50,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(25),
        border: Border.all(
          color: Colors.grey[300]!,
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          const SizedBox(width: 16),
          Icon(
            Icons.search,
            color: Colors.grey[600],
            size: 24,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: TextField(
              controller: _controller,
              focusNode: _focusNode,
              decoration: InputDecoration(
                hintText: widget.hintText ?? 'Rechercher un produit...',
                hintStyle: EcoTypography.bodyMedium.copyWith(
                  color: Colors.grey[400],
                ),
                border: InputBorder.none,
                isDense: true,
              ),
              style: EcoTypography.bodyMedium,
            ),
          ),
          if (_hasText)
            IconButton(
              icon: Icon(Icons.clear, color: Colors.grey[600], size: 20),
              onPressed: _clearText,
            )
          else
            const SizedBox(width: 8),
        ],
      ),
    );
  }
}

